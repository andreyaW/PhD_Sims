import numpy as np
import inspect
import copy


def random_to_R_t(random_fail_times: np.array): 
    ''' Arranges the random failure times into a reliability curve
    Params:
        failure_times(ndarray): 
            an array of random times to failure
    Returns:
        R_t (ndarray): 
            generated reliability curve, (approximated CDF) 
        t (ndarray): 
            times associated with the reliability curve
    '''
    # sort failure times in ascending order
    random_fail_times.sort() 
        
    # create a dummy varaible to solve R_t
    R_t = np.empty_like(random_fail_times)
    t= np.empty_like(random_fail_times)
    num_samples = len(random_fail_times)

    # solve for the probability of failure and reliability at each time
    for i, hours in enumerate(random_fail_times):
    
        # save each time as a sample point, replace negative values with zeros
        if t[i] > 0:
            t[i] = hours
        else:
            t[i] = 0.0
        
        # solve for the probability of failure (p(failure)) at each time
        p_fail = (i+1) / num_samples
        # solve for the reliability (1 - p(failure)) at each time
        R_t[i] = (1-  p_fail)        # (aka the approximate CDF of the random failure times)

    return R_t, t



def find_times_less_than(failure_times, time_to_lookup):
    ''' Finds the closest time left of the requested lookup time
    Params: 
        failure_times: increasing array of failure times
        time_to_lookup: time to compute the failure at
    Returns:
        indexFound: index of largest value in failure_times that is less than time_to_lookup
    '''
    
    #search for the time index in the random failure times closest to the desired time
    indexFound= np.searchsorted(failure_times, time_to_lookup, side="right") - 1

    #if no time is found the desired time is outside of the originally generated reliability 
    #distribution, do something....
    if indexFound == -1:

        #determine if the lookup time is to the left or right of the generated distribution
        first_random_fail= failure_times[0]
        last_random_fail= failure_times[-1]

        #if lookup times > random failure times then the component has most likely failed already
        if time_to_lookup > last_random_fail: 
            #indexFound= np.where(failure_times == failure_times[-1]) #match to final failure probability
            indexFound=len(failure_times)-1
            
        #if lookup times < random failure times then the component is most likely working still
        elif time_to_lookup < first_random_fail: 
            
            #indexFound= np.where(failure_times == failure_times[0]) #match to final failure probability
            indexFound=0
        else: 
            print("there is an error in the component distribution or the lookup times requested. See findTimesLessThan in components.py")

    return indexFound




def find_lookup_R_t(R_t, t, lookup_t, failing_parts = None):
    ''' Takes a R_t curve of random times and finds the R_t along a lookup array of times also
        stores the part reqponsible for the failure at each time (for systems or comp groups)
    Params: 
        R_t: random array of reliabilities over time (arranged decreasing but not evenly spaced sample points)
        t: times associated with each random R_t
        time_to_lookup: time to compute the failure at
        failing_parts: the parts responsible for each R_t along the curve
    Returns:
        lookup_R_t: R_t along the lookup times
        lookup_t: times used for the R_t lookup
        failing_parts: part responsible for each found lookup R_t
    '''
    
    #find times along the generated R_t curve that is closest to desired lookup times        
    found_t = [0 for i in range(len(lookup_t))]
    lookup_R_t = [0 for i in range(len(lookup_t))]
    failing_part = [0 for i in range(len(lookup_t))]

    for i,lookup_time in enumerate(lookup_t):
        # print('lookup times is ', lookup_time)
        # print('i is', i)
        
        #find the next time of failure closest to the look up time
        found_t[i] = find_times_less_than(t, lookup_time)       

        # grab the portion of the R_t curve that is desired
        lookup_R_t[i] = R_t[found_t[i]]
        
        if failing_parts!= None: 
            failing_part[i] = failing_parts[found_t[i]]        
    
    if failing_parts is None: 
        return lookup_R_t , lookup_t   
    else:
        return lookup_R_t , lookup_t, failing_part      




def determine_R_t_from_multiple_r_ts( many_R_ts, many_ts):
    ''' from a matrix of R_t curves, determine the resultant R_t of the group or system
    Params: 
        many_R_ts: random array of reliabilities over time (arranged decreasing but not evenly spaced sample points)
        many_ts: times associated with each random R_t
    Returns:
        R_t: the lowest reliability at each most immediate time step
        t: time steps associated with the selected R_t
        failing_object: part responsible for each selected R_t
    '''
    
    # store the first minimum failure time and reliability
    i = 0
    R_t = []
    t = []
    failing_object = []

    # first handling cases where comp fails at zero
    indices = np.where(many_ts == 0)
    if any(len(arr) == 0 for arr in indices): 
        pass
    else:
        indices_list =  list(zip(indices[0], indices[1]))
        t_equal_zero_R_t = []
        for index in indices_list: 
            t_equal_zero_R_t.append(many_R_ts[index])
            failing_object.append(index[0])
        R_t = sorted(t_equal_zero_R_t, reverse= True)
        t = [0 for i in range(len(t_equal_zero_R_t))]

    # check for the next highest t value after zero
    current_t = 0 

    if len(R_t) == 0 :
        R_t.append(1.0)    #no parts fail at zero so 100% reliability to start
        t.append(0)
        failing_object.append(0)

    final_low_t_index = np.argmin(many_ts[:,-1])        
    while R_t[-1] != many_R_ts[final_low_t_index, -1]:

        # Mask the matrix to find all times greater than the current time
        mask = (many_ts > current_t)

        # determine the minimum of the higher times
        higher_times= many_ts[mask]
        min_higher_t = np.min(higher_times)
        
        # Use np.argwhere to find the index of the next higher t
        min_higher_t_index = np.argwhere(many_ts == min_higher_t)
        
        # if the R_t at the next higher t is less than the previous R_t then add it to the sys R_t
        if many_R_ts[min_higher_t_index[0][0], min_higher_t_index[0][1]] < R_t[-1]:
            R_t.append(many_R_ts[min_higher_t_index[0][0], min_higher_t_index[0][1]])
            t.append(min_higher_t)

            # for each system reliability time found, store also the index of the component causing failure 
            failing_object.append(min_higher_t_index[0][0])
                        
            #replace the current time being checked
            current_t = min_higher_t

        else:
            
            #replace the current time being checked
            current_t = min_higher_t
            
    return R_t, t, np.array(failing_object)



def determine_fail_rate(object , operational_time):
    '''determine the number of times each component or component group will fail in a given period
    Params:
        object: a component group or system
        operational_time: the time to check the average failures over
    Returns:
        fails_during_operation: count of how many times a part will fail in an operational period     
    '''

    # ensure the average failure times exist for each part
    # determine_average_failure_t(object)
    
    # number of times the failure will occur in the operational period
    fail_rates= []
    # print(len(object.parts))
    for part in object.parts:
        if inspect.getmodule(part).__name__ == 'Model.model_component_groups':
            FR = part.fail_rate
            fail_rates.append(FR)
        else:
            # life_span = part.t_solved[-2] - part.t_solved[1]
            life_span2 = part.t[-1] - part.t[0]
            FR = operational_time / life_span2
            fail_rates.append(FR)
            part.fail_rate = FR

    for part in object.series_parts:
        if inspect.getmodule(part).__name__ == 'Model.model_component_groups':
            FR = part.fail_rate
        else:
            # life_span = part.t_solved[-2] - part.t_solved[1]
            life_span2 = part.t[-1] - part.t[0]
            FR = operational_time / life_span2
            part.fail_rate = FR

            
    # save the objects number of fails during operation
    highest_fail_rate= np.average(fail_rates)
    # print(np.argmax(fail_rates))

    object.fail_rate = highest_fail_rate


def determine_MTBF(object):
    ''' Determine the average time of failure of the given object
    Params:
        object (component, component_group, system): 
            can be a component, component group or system
    Returns:
        avg_failure_t (float) : 
            the average time of failure of the system, normalized by mission length if length is provided
    '''
    MTBF = sum(object.t) / len(object.t)
    object.MTBF = MTBF


def grab_instance(random_fail_times, num_realization):
    '''Determine the failure realization time for the desired ship instance
    Params:
        num_realization: the "failure instance" or "vessel number" to select from the randomly generated
                         distribution of serial component failure times . 

    Returns:
        fail_time: the time of failure for the instance requested        
    '''
    #grab a failure instance from original random distribution
    fail_time = random_fail_times[num_realization]
    
    if fail_time<0: 
        fail_time= 0.0

    return fail_time  
  

def mission_success_test(target_op_time, object):
    ''' determine how many simulated failures occur after the mission length
    Params:
        target_op_time : the objective operational time to determine the number of failures that occur after
        object : a group of components, system or ship object 
    Returns:
        success_rate: percentage of simulated failures that occur after the target_op_time
    '''
    if inspect.getmodule(object).__name__ == 'Model.model_component_groups' or   inspect.getmodule(object).__name__ == 'Model.model_system':
        
        # determine the number of failurs on the R(t) curve that are to the right of the target time
        fail_times = np.array(copy.copy(object.t))
        post_target_fails = fail_times[fail_times > target_op_time]
        
    success_rate = len(post_target_fails) / object.sample_size
            
    # return percentage of sucessful ships
    return success_rate

