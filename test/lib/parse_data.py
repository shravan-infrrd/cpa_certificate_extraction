from lib.helpers.parse_name import ParseName
from lib.helpers.parse_credits import ParseCredits
from lib.helpers.parse_field_of_study import ParseFieldOfStudy
from lib.helpers.parse_fos import ParseFos
from lib.helpers.parse_date import ParseDate
from lib.helpers.parse_completion_date import ParseCompletionDate
from lib.helpers.parse_delivery_methods import ParseDeliveryMethod
from lib.helpers.parse_sponsors import ParseSponsors
from lib.helpers.parse_sponsor_id import ParseSponsorId
from lib.helpers.parse_program_name import ParseProgramName
from lib.helpers.parse_qas_number import ParseQasNumber

def parse_all_fields( contents, result):
    pn = ParseName(contents)
    pn.extract()

    pp = ParseProgramName(contents, pn.name)
    pp.extract()

    pd  = ParseDate(contents, pn.name, pp.program_name)
    pd.extract()

    """
    pf = ParseFieldOfStudy(contents)
    pf.extract()
    """

    pfos = ParseFos(contents)
    pfos.extract()

    pc = ParseCredits(contents, pfos.field_of_study)
    pc.extract()



    #pcod = ParseCompletionDate(contents)
    #pcod.extract()

    pm = ParseDeliveryMethod(contents)
    pm.extract()

    ps = ParseSponsors(contents)
    ps.extract()

    pi = ParseSponsorId(contents)
    pi.extract()

    pq = ParseQasNumber(contents)
    pq.extract()





    result['name']            = pn.name
    result['program_name']    = pp.program_name
    #result['field_of_study']  = pf.field_of_study
    result['credits']         = pc.credits
    result['date']            = pd.date
    #result['completion_date'] = pd.date
    result['delivery_method'] = pm.delivery_method
    result['sponsor']         = ps.sponsor
    result['sponsor_id']      = pi.sponsor_id
    #result['sponsor_id']      = pi.ids
    result['qas_number']      = pq.qas_number
    #result['fos']             = pfos.field_of_study
    result['fos']             = pc.field_of_study

    print("RESULT====>", result)
    return result
