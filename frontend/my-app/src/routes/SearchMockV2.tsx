import {
  Button,
  Center,
  Divider,
  Flex,
  HStack,
  Heading,
  Input,
  Skeleton,
  Spinner,
  Stack,
  VStack,
} from "@chakra-ui/react";
import MovieCardWithImage from "../ui/MovieCard";
import { CompactMovieData, MovieDataWithTrailer } from "../types";
import { useState } from "react";

const dummyMovie: MovieDataWithTrailer = {
  title: "Star Wars: Episode IV - A New Hope",
  year: "1977",
  rated: "PG",
  released: "25 may 1977",
  runtime: "121 min",
  genre: "Action, Fantasy",
  director: "George Lucas",
  plot: "rofl",
  poster:
    "https://m.media-amazon.com/images/M/MV5BOTA5NjhiOTAtZWM0ZC00MWNhLThiMzEtZDFkOTk2OTU1ZDJkXkEyXkFqcGdeQXVyMTA4NDI1NTQx._V1_SX300.jpg",
  imdbrating: "8.6",
  imdbid: "tt123341232",
  trailerLink: "https://www.youtube.com/watch?v=vZ734NWnAHA",
};
export default function SearchMockV2() {
  const [title, setTitle] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [compactMovieData, setCompactMovieData] = useState<CompactMovieData[]>(
    []
  );
  const [moviesWithTrailer, setMoviesWithTrailer] = useState<
    MovieDataWithTrailer[]
  >([]);
  const [error, setError] = useState("");

  async function searchMovies(query: string) {
    setCompactMovieData([]);
    setCompactMovieData([]);
    const URL = "http://localhost:8000/mock/v2/trailer/search";

    try {
      setIsLoading(true);
      const response = await fetch(`${URL}?title=${query}&network_lag=0`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: query }),
      });
      if (response.ok) {
        const data = await response.json();
        setCompactMovieData(data);

        const dataArray = [];

        for (const movie of data) {
          const response = await fetch(
            `${URL}/${movie.imdbid}?network_lag=1.2`,
            {
              method: "POST",
              headers: {
                "content-type": "application/json",
              },
              body: JSON.stringify({ title: movie.title }),
            }
          );

          const result = await response.json();
          dataArray.push(result);
          console.log("result is", result);
          console.log("array is now: ", dataArray);
          setMoviesWithTrailer([...dataArray]);
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Flex
      height="100vh"
      justifyContent="flex-start"
      alignItems="center"
      flexDirection="column"
    >
      <Heading mb={4}>Search Trailers</Heading>
      <Flex width="50%" mb={10}>
        <Input
          placeholder="Enter your search term"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          flex="1"
          mr={2}
        />
        <Button onClick={() => searchMovies(title)} colorScheme="teal">
          Search
        </Button>
      </Flex>
      <Flex flexDir={"column"} gap={5}>
        {moviesWithTrailer &&
          moviesWithTrailer.map((movie) => {
            return (
              <>
                <MovieCardWithImage movie={movie} />
                <Divider height={10} colorScheme="teal" />
              </>
            );
          })}
        {/* <MovieCardWithImage movie={dummyMovie} /> */}
        {/* <MovieCardWithImage movie={dummyMovie} /> */}
        {isLoading && (
          <Center>
            {/* <Spinner size={"xl"} /> */}
            <Stack>
              <Skeleton width="600px" height="20px" />
              <Skeleton width="600px" height="20px" />
              <Skeleton width="600px" height="20px" />
              <Skeleton width="600px" height="20px" />
              <Skeleton width="600px" height="20px" />
              <Skeleton width="600px" height="20px" />
            </Stack>
          </Center>
        )}
      </Flex>
    </Flex>
  );
}

// export default function SearchMockV2() {
//   return (
//     <VStack spacing={12} width="100%" marginX="auto">
//       <Heading as="h1" size="xl">
//         Search Trailers
//       </Heading>
//       <HStack>
//         <Input placeholder="Search..." w="full" mr={2} />
//         <Button colorScheme="teal" size="sm">
//           Search
//         </Button>
//       </HStack>
//     </VStack>
//   );
// }
