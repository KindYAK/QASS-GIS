import {GEOSERVER_WMS_URL, ROOT_API} from "~/settings/settings.js";

export default function ({ $axios }, inject) {
  // Create a custom axios instance
  const apiClient = $axios.create({
    withCredentials: false,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

  const api = {
    getRegions: async () => {
      return await apiClient({url: `regions/`, baseURL: ROOT_API, method: 'GET'});
    },
    callGetFeatureInfo: async (url) => {
      return await apiClient({url: url, baseURL: GEOSERVER_WMS_URL, method: 'GET'});
    }
  };

  // Inject to context as $api
  inject("api", api);
}
