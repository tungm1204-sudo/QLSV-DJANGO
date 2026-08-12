import { useQuery } from '@tanstack/react-query';
import * as api from '../api/masterDataApi';

const createOptionHook = (queryKey, apiObj) => {
  return () => {
    return useQuery({
      queryKey: ['master-data-options', queryKey],
      queryFn: async () => {
        // Fetch all active items, assume max_page_size=1000
        const res = await apiObj.getAll({ page_size: 1000 });
        const results = res.data?.results || res.data || [];
        return results.map(item => ({
          value: item.id,
          label: item.name || item.code || item.id,
          // Bổ sung code để hiển thị nếu có
          code: item.code
        }));
      },
      staleTime: 5 * 60 * 1000, // Cache for 5 minutes
    });
  };
};

export const useMajorOptions = createOptionHook('majors', api.majorApi);
export const useDepartmentOptions = createOptionHook('departments', api.departmentApi);
export const useAdministrativeClassOptions = createOptionHook('administrativeClasses', api.administrativeClassApi);
export const useEducationSystemOptions = createOptionHook('educationSystems', api.educationSystemApi);
export const useAdmissionTypeOptions = createOptionHook('admissionTypes', api.admissionTypeApi);
export const usePriorityCategoryOptions = createOptionHook('priorityCategories', api.priorityCategoryApi);
export const useCohortOptions = createOptionHook('cohorts', api.cohortApi);
export const useEthnicityOptions = createOptionHook('ethnicities', api.ethnicityApi);
export const useReligionOptions = createOptionHook('religions', api.religionApi);
export const useNationalityOptions = createOptionHook('nationalities', api.nationalityApi);
export const useDegreeOptions = createOptionHook('degrees', api.degreeApi);
export const useAcademicTitleOptions = createOptionHook('academicTitles', api.academicTitleApi);
export const usePositionOptions = createOptionHook('positions', api.positionApi);
