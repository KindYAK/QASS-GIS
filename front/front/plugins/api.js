export default function ({ $axios, $config: {apiURL} }, inject) {
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
      return await apiClient({url: `regions/`, baseURL: apiURL, method: 'GET'});
    },
  };

  // Inject to context as $api
  inject("api", api);
}
