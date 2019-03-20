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





    result['name']            = {"value": pn.name, "score": ""}
    result['program_name']    = {"value": pp.program_name, "score": ""}
    #result['field_of_study']  = pf.field_of_study
    result['credits']         = {"value": pc.credits, "score": ""}
    result['date']            = {"value": pd.date, "score": ""}
    #result['completion_date'] = pd.date
    result['delivery_method'] = {"value": pm.delivery_method, "score": "" }
    result['sponsor']         = [{"value": ps.sponsor, "score": "" }]
    result['sponsor_id']      = [{"value": pi.sponsor_id, "score": "" }]
    #result['sponsor_id']      = pi.ids
    result['qas_number']      = {"value": pq.qas_number, "score": ""}
    #result['fos']             = pfos.field_of_study
    result['fos']             = {"value": pc.field_of_study, "score": ""}

    print("RESULT====>", result)
    return result
