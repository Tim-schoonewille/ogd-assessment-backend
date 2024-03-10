import { useEffect, useState } from "react";
import { CompactMovieData, MovieDataWithTrailer } from "../types";
import { Button, Input, Link, Spinner } from "@chakra-ui/react";

export default function MockSearchPageV2() {
  const [title, setTitle] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [compactMovieData, setCompactMovieData] = useState<CompactMovieData[]>(
    []
  );

  const [moviesWithTrailer, setMoviesWithTrailer] =
    useState<MovieDataWithTrailer[]>();

  async function searchMovies(query: string) {
    const URL = "http://localhost:8000/mock/v2/trailer/search";
    try {
      setIsLoading(true);
      const response = await fetch(`${URL}?title=${query}&network_lag=0`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      setCompactMovieData(data);

      const dataArray = [];

      for (const movie of data) {
        const response = await fetch(`${URL}/${movie.imdbid}`, {
          method: "POST",
          headers: {
            "content-type": "application/json",
          },
          body: JSON.stringify({ title: movie.title }),
        });

        const result = await response.json();
        dataArray.push(result);
        console.log("result is", result);
        console.log("array is now: ", dataArray);
        setMoviesWithTrailer([...dataArray]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }

  //   useEffect(() => {
  //     searchMovies("lord of the rings");
  //   }, []);

  return (
    <>
      <h1>Hello world!</h1>
      <Input value={title} onChange={(e) => setTitle(e.target.value)} />
      <Button onClick={() => searchMovies(title)}>Let's go!!</Button>

      {moviesWithTrailer && (
        <ul>
          {moviesWithTrailer.map((movie) => {
            return (
              <li key={movie.imdbid}>
                {movie.title}
                <br />
                {movie.trailerLink}
              </li>
            );
          })}
        </ul>
      )}
      {isLoading && <Spinner />}
    </>
  );
}
