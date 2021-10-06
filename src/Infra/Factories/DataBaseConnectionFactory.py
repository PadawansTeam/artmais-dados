class DataBaseConnectionFactory():
    def Create():
        POSTGRES = {
            'user': '##',
            'pw': '##',
            'db': '#',
            'host': '##',
            'port': '##',
        }

        SQLALCHEMY_DATABASE_URL = 'postgresql://%(user)s:\
        %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

        engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        Base = declarative_base()

        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        return Session()
