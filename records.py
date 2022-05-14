import datetime


class Memories:
    def __init__(self, first_date=None, name=None, records=None):
        self.first_date = first_date or datetime.date.today()
        self.name = name or ""
        self.records = records or []

    def save_as_yaml(self, name):
        from yaml import dump, CDumper
        meta = self.__dict__.copy()
        meta["records"] = [
            {"class": record.__class__.__name__, "data": record.to_dict()}
            for record in self.records
        ]
        dump(meta, open(f"{name}.yaml", "w"), CDumper)

    @classmethod
    def load_from_yaml(cls, name):
        from yaml import load, CLoader
        meta = load(open(f"{name}.yaml"), CLoader)
        new = cls(**meta)
        new.records = [eval(i["class"]).from_dict(i["data"]) for i in new.records]
        return new

    def save_as_pickle(self, name):
        from pickle import dump, HIGHEST_PROTOCOL
        dump(self, open(f"{name}.pkl", "wb"), HIGHEST_PROTOCOL)

    @classmethod
    def load_from_pickle(cls, name):
        from pickle import load
        return load(open(f"{name}.pkl", "rb"))

    @staticmethod
    def save_as_zip():
        return NotImplemented

    def append(self, record):
        self.records.append(record)

    def find_records_by_date(self, date: datetime.date) -> list["Record"]:
        return list(filter(lambda record: record.date == date, self.records))

    def find_records_by_title(self, title: str) -> list["Record"]:
        return list(filter(lambda record: record.title == title, self.records))

    def find_records_by_tags(self, *tags, method="all") -> list["Record"]:
        tags = set(tags)
        if method == "all":
            return list(filter(lambda record: tags < set(record.tags), self.records))
        elif method == "any":
            return list(filter(lambda record: tags & set(record.tags), self.records))
        else:
            return NotImplemented

    def __repr__(self):
        return f"Memories[{len(self.records)}]<{self.name}> from {self.first_date}"


class Record:
    tags: list
    title: str
    image: str
    date: datetime.date

    def __repr__(self):
        return f"Record< {self.title} @ date={self.date} >"

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        new = Record()
        new.__dict__.update(data)
        return new


class ImgSeqRecord(Record):
    def __init__(self, images=None):
        self.images = images or []
        super().__init__()

    @property
    def image(self):
        return self.images[0]

    def __repr__(self):
        return f"ImgSeqRecord[{len(self.images)}]< {self.title} @ {self.date} >"
