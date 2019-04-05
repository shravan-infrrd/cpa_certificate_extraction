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

    ps = ParseSponsors(contents, pp.program_name)
    ps.extract()

    pd  = ParseDate(contents, pn.name, pp.program_name)
    pd.extract()

    pfos = ParseFos(contents, pp.program_name)
    pfos.extract()

    pc = ParseCredits(contents, pfos.field_of_study)
    pc.extract()

    pm = ParseDeliveryMethod(contents)
    pm.extract()

    pi = ParseSponsorId(contents)
    pi.extract()

    pq = ParseQasNumber(contents)
    pq.extract()





    result['username']            = {"value": pn.name, "score": ""}
    result['program_name']    		= {"value": pp.program_name, "score": ""}
    #result['field_of_study']  		= pf.field_of_study
    result['credits']         		= {"value": pc.credits, "score": ""}
    result['completion_date']     = {"value": pd.date, "score": ""}
    #result['completion_date'] 		= pd.date
    result['delivery_format'] 		= {"value": pm.delivery_method, "score": "" }
    result['sponsor_name']        = [{"value": ps.sponsor, "score": "" }]
    result['sponsor_number']      = [{"value": pi.sponsor_id, "score": "" }]
    #result['sponsor_id']      		= pi.ids
    result['qas_number']      		= {"value": pq.qas_number, "score": ""}
    #result['fos']             		= pfos.field_of_study
    result['field_of_study']      = pc.field_of_study #{"value": pc.field_of_study, "score": ""}

    print("RESULT====>", result)
    return result
