import cProfile
import get_data
import write_into_excel
cProfile.run('get_data')
cProfile.run('write_into_excel')
cProfile.run('transform_into_vision')