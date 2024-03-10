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

export default function SearchV2() {
  const [title, setTitle] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [compactMovieData, setCompactMovieData] = useState<CompactMovieData[]>(
    []
  );
  const [moviesWithTrailer, setMoviesWithTrailer] = useState<
    MovieDataWithTrailer[]
  >([]);

  async function searchMovies(query: string) {
    setCompactMovieData([]);
    setCompactMovieData([]);
    const URL = "http://localhost:8000/api/v2/trailer/search";

    try {
      setIsLoading(true);
      const response = await fetch(`${URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: query }),
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

  return (
    <Flex
      height="100vh"
      justifyContent="flex-start"
      alignItems="center"
      flexDirection="column"
    >
      <Heading mb={4}>Search Trailers v2</Heading>
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

        {isLoading && (
          <Center>
            <Spinner />
            <Stack>
              <Skeleton height="20px" />
              <Skeleton height="20px" />
              <Skeleton height="20px" />
            </Stack>
          </Center>
        )}
      </Flex>
    </Flex>
  );
}
