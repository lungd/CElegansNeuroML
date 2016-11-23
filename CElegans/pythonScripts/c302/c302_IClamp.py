import c302
import sys
    
def setup(parameter_set, 
          generate=False,
          duration=2500,
          dt=0.05,
          target_directory='examples'):

    exec('from parameters_%s import ParameterisedModel'%parameter_set)
    params = ParameterisedModel()
    
    params.set_bioparameter("unphysiological_offset_current", "2pA", "Testing IClamp", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "100 ms", "Testing IClamp", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "2000 ms", "Testing IClamp", "0")
    
    
    my_cells = ["AVM",]
    my_cells = ["AVM"]
    include_muscles = False
    
    cells               = my_cells
    cells_to_stimulate  = ["AVM"]
    
    reference = "c302_%s_IClamp"%parameter_set
    
    if generate:
        c302.generate(reference, 
                    params, 
                    cells=cells, 
                    cells_to_stimulate=cells_to_stimulate, 
                    include_muscles = include_muscles,
                    duration=duration, 
                    dt=dt, 
                    validate=('B' not in parameter_set),
                    target_directory=target_directory)
                    
    return cells, cells_to_stimulate, params, include_muscles
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)
