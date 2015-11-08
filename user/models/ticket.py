#! -*- coding:utf8 -*-
# ticket
#
import sys
sys.path.append("../..")
from base.db_helper import DB42
from base.entity_id_helper import EntityIdHelper
import time

class Ticket(object):
    def __init__(self, id, user_id, create_time):
        self.id = id
        self.user_id = user_id
        self.create_time = create_time

class TicketDAO(object):
    def __init__(self):
        self._db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'user')

    def GetByUser(self, user_id):
        SQL = "select * from ticket where user_id  = %s" % user_id
        result = self._db.query(SQL)
        print result
        # TODO (1L, 1L, 123141124124) to Ticket
        tickets = []
        if result[0]:
            for eachItem in result[1]:
                tickets.append(Ticket(eachItem[0], eachItem[1], eachItem[2]))
        else:
            tickets.append(Ticket(result[1][0], result[1][1], result[1][2]))
        return tickets

    def InsertOrUpdate(self, user_id, create_time):
        params = [user_id, create_time, create_time]
        result = self._db.update("insert into ticket(user_id, create_time) values(%s, %s) on duplicate key update create_time = %s", params)
        return result

class TicketService(object):
    @classmethod
    def create_ticket(self, user_id, create_time):
        dao = TicketDAO()
        new_id = dao.InsertOrUpdate(user_id, create_time)
        if new_id:
            return "|".join([EntityIdHelper().encode(new_id, 'Ticket'), EntityIdHelper().encode(user_id, 'User'), EntityIdHelper().encode(create_time, 'Ticket')])
        return None

    @classmethod
    def verify_ticket(self, ticket):
        if not ticket:
            return False
        dao = TicketDAO()
        parts = ticket.split("|")
        if parts and parts[1]:
            result = dao.GetByUser(EntityIdHelper().decode(parts[1],'User'))
            if result:
                tid = EntityIdHelper().decode(parts[0],'Ticket')
                ct = float(EntityIdHelper().decode(parts[2],'Ticket'))
                return long(tid) == result[0].id and int(round(ct)) == result[0].create_time
        return False

    @classmethod
    def get_ticket(self, user_id):
        if not user_id:
            return None
        dao = TicketDAO()
        result = dao.GetByUser(user_id)
        if result:
            return "|".join([EntityIdHelper().encode(result[0].id, 'Ticket'), EntityIdHelper().encode(user_id, 'User'), EntityIdHelper().encode(result[0].create_time, 'Ticket')])
        return None

if __name__ == '__main__':
    x = TicketService.create_ticket(1,time.time())
    print x
    print TicketService.verify_ticket(x)
