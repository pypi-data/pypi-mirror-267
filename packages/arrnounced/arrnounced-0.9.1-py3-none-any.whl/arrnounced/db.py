from datetime import datetime, timedelta
import logging
import os
import threading

from pony.orm import Database, desc, pony, Required, Set
from pony.orm import db_session  # noqa: F401

logger = logging.getLogger("DB")
db = Database()


class Announced(db.Entity):
    date = Required(datetime)
    title = Required(str)
    indexer = Required(str)
    torrent = Required(str)
    backend = Required(str)
    snatched = Set("Snatched")

    def serialize(self, transform_date):
        return {
            "id": self.id,
            "date": transform_date(self.date),
            "title": self.title,
            "indexer": self.indexer,
            "torrent": self.torrent,
            "backend": self.backend,
        }


class Snatched(db.Entity):
    date = Required(datetime)
    announced = Required(Announced)
    backend = Required(str)


def init(destination_dir):
    try:
        db.bind(
            "sqlite",
            os.path.join(os.path.realpath(destination_dir), "brain.db"),
            create_db=True,
        )
        db.generate_mapping(create_tables=True)
    except pony.orm.dbapiprovider.OperationalError as e:
        logger.error(
            "Could not initiate database: %s",
            e,
        )
        return False

    return True


def snatched_to_dict(snatched, transform_date):
    return {
        "date": transform_date(snatched[1]),
        "indexer": snatched[2],
        "title": snatched[3],
        "backend": snatched[4],
    }


def get_snatched(limit, page):
    # Order by first attribute in tuple i.e. s.id
    ss = (
        pony.orm.select(
            (s.id, s.date, a.indexer, a.title, s.backend)
            for s in Snatched
            for a in s.announced
        )
        .order_by(desc(1))
        .limit(limit, offset=(page - 1) * limit)
    )
    return ss


def get_announced(limit, page):
    return (
        Announced.select()
        .order_by(desc(Announced.id))
        .limit(limit, offset=(page - 1) * limit)
    )


def get_announcement(id):
    return Announced.get(id=id)


def insert_announcement(announcement, backends):
    return Announced(
        date=announcement.date,
        title=announcement.title,
        torrent=announcement.torrent_url,
        indexer=announcement.indexer,
        backend=backends,
    )


def insert_snatched(announcement, date, backend):
    Snatched(date=date, announced=announcement, backend=backend)


def get_announced_count():
    return pony.orm.count(a for a in Announced)


def get_snatched_count():
    return pony.orm.count(s for s in Snatched)


@db_session
def get_latest(indexer):
    latest_a = (
        Announced.select(lambda a: a.indexer == indexer).order_by(desc(1)).limit(1)
    )
    latest_s = (
        pony.orm.select(
            (s.id, s.date)
            for s in Snatched
            for a in s.announced
            if a.indexer == indexer
        )
        .order_by(desc(1))
        .limit(1)
    )

    return (
        None if len(latest_a) == 0 else latest_a[0].date,
        None if len(latest_s) == 0 else latest_s[0][1],
    )


_stop_thread = threading.Event()


def stop():
    logger.debug("Stopping database purge thread")
    _stop_thread.set()


def run(user_config):
    one_day = 24 * 60 * 60
    running = user_config.db_purge_days > 0
    while running:
        with db_session:
            old_date = datetime.now() - timedelta(days=user_config.db_purge_days)
            snatched_rows = db.execute(
                "DELETE FROM Snatched WHERE announced IN "
                "(SELECT Announced.id FROM Announced "
                "INNER JOIN Snatched ON Snatched.announced = Announced.id "
                "WHERE Announced.date < $old_date)"
            ).rowcount
            announced_rows = db.execute(
                "DELETE FROM Announced WHERE date < $old_date"
            ).rowcount

            if announced_rows > 0:
                logger.info(
                    "Purged %s announcements older than %s from the database, %s of which where snatched",
                    announced_rows,
                    old_date,
                    snatched_rows,
                )

        running = not _stop_thread.wait(timeout=one_day)
    logger.info("Purge thread finished")
