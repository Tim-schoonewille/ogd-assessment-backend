import {
  Button,
  Center,
  Divider,
  Flex,
  HStack,
  Heading,
  Icon,
  Input,
  Skeleton,
  Spinner,
  Stack,
  VStack,
} from "@chakra-ui/react";
import MovieCardWithImage from "../ui/MovieCard";
import { CompactMovieData, MovieDataWithTrailer } from "../types";
import { FormEvent, useState } from "react";
import { BiCameraMovie } from "react-icons/bi";

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
            `${URL}/${movie.imdbid}?network_lag=0.3`,
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
    <>
      <Flex
        justifyContent="flex-start"
        alignItems="center"
        flexDirection="column"
      >
        <Flex>
          <Heading>
            <Icon mr={3} as={BiCameraMovie} />
          </Heading>
          <Heading mb={4}>Search Trailers</Heading>
        </Flex>
        <Flex
          as="form"
          width="50%"
          mb={10}
          onSubmit={(e) => {
            e.preventDefault();
            searchMovies(title);
          }}
        >
          <Input
            placeholder="Enter your search term"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            flex="1"
            mr={2}
          />
          <Button type="submit" colorScheme="teal">
            Search
          </Button>
        </Flex>
      </Flex>
      <Flex
        flexDir={"column"}
        gap={5}
        alignItems={"center"}
        flexDirection="column"
      >
        {moviesWithTrailer &&
          moviesWithTrailer.map((movie) => {
            return (
              <>
                <MovieCardWithImage movie={movie} />
                <Divider height={2} w="600px" colorScheme="teal" />
              </>
            );
          })}
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
    </>
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
