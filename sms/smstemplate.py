TEMPLATE_LIST = (
    ('', '----------------'),
    ('1', 'Sales Invoice'),
    ('2', 'Purchase Bill Payment'),
    ('3', 'Member Admission'),
    ('4', 'Deposit Receive'),
    ('5', 'Deposit Payment'),
    ('6', 'Loan Disbursement'),
    ('7', 'Loan Installment Receive'),
    ('8', 'Loan Installment Due'),
    ('9', 'Loan Installment Overdue'),
    ('10', 'Loan Installment Receive From Deposit'),
    ('11', 'FDR Open'),
    ('12', 'DPS Open'),
    ('13', 'FDR Profit Transfer'),
    ('14', 'Deposit Profit Transfer'),
    ('15', 'FDR Closing'),
    ('16', 'DPS Closing'),
    ('17', 'Savings Open'),
    ('18', 'Savings Closing'),
    ('20', 'Share Receive'),
    ('21', 'Share Payment'),
    ('22', 'DPS Receive'),
    ('23', 'DPS Payment'),
    ('00', 'Manual SMS Send'),
)

MESSAGE_TYPE = (
    ('text', 'Text'),
    ('unicode', 'Unicode'),
)

MESSAGE_LABEL = (
    ('transactional', 'Transactional'),
    ('promotional', 'Promotional'),
)

TEMPLATE_DICT = dict((x, y) for x, y in TEMPLATE_LIST)