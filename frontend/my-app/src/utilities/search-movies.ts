export async function searchMovies(query: string) {
  const URL = "http://localhost:8000/mock/v2/trailer/search/";
  try {
    const response = await fetch(`${URL}?title=${query}&network_lag=0`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log(data);
    return data;
  } catch (e) {
    console.error(e);
  }
}
