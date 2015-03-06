from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities     import VCardMediaMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
import logging
logger = logging.getLogger(__name__)

class SendVCardLayer(YowInterfaceLayer):

    PROP_TO = "org.openwhatsapp.yowsup.prop.sendclient.to"

    def __init__(self):
        super(SendVCardLayer, self).__init__()
        self.ackQueue = []

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        vcard_data = """BEGIN:VCARD
(Your VCard Data here)
END:VCARD
"""
        phone = self.getProp(self.__class__.PROP_TO)
        outVcard = VCardMediaMessageProtocolEntity('VcardName', vcard_data, to = phone + "@s.whatsapp.net")
        self.ackQueue.append(outVcard.getId())
        self.toLower(outVcard)


    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            logger.info("VCard sent")
            raise KeyboardInterrupt()

