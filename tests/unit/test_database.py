import datetime

from modules.models import TronInfo


class TestDatabase:
    def test_add_tron_info(self, db_session):
        test_data = TronInfo(
            address='TRfsdfitr656FFGkL9',
            bandwidth=10000,
            energy=1234,
            trx_balance=934750,
            timestamp=datetime.datetime.now(datetime.UTC).isoformat(sep=' ', timespec='seconds')
        )

        db_session.add(test_data)
        db_session.commit()

        res = db_session.query(TronInfo).filter_by(address=test_data.address).first()

        assert res is not None
        assert res.bandwidth == test_data.bandwidth
        assert res.energy == test_data.energy
        assert res.trx_balance == test_data.trx_balance

        db_session.delete(res)
        db_session.commit()


