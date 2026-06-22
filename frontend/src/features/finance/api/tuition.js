import axiosClient from "../../../api/axiosClient";

export const tuitionApi = {
  getTuitionFees: () => axiosClient.get("finance/tuition/"),
  payTuitionFee: (id) => axiosClient.post(`finance/tuition/${id}/pay/`),
};
