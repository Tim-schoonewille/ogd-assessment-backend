import {
  Button,
  Center,
  Divider,
  Flex,
  HStack,
  Heading,
  Icon,
  Input,
  ScaleFade,
  Skeleton,
  Spinner,
  Stack,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import MovieCardWithImage from "../ui/MovieCard";
import { CompactMovieData, MovieDataWithTrailer } from "../types";
import { FormEvent, useState } from "react";
import { BiCameraMovie } from "react-icons/bi";

export default function SearchMockV2() {
  const [title, setTitle] = useState("");
  const [networkLag, setNetworkLag] = useState("1.2");
  const [isLoading, setIsLoading] = useState(false);
  const [compactMovieData, setCompactMovieData] = useState<CompactMovieData[]>(
    []
  );
  const [moviesWithTrailer, setMoviesWithTrailer] = useState<
    MovieDataWithTrailer[]
  >([]);
  const [errorData, setErrorData] = useState("");
  const [errorFlag, setErrorFlag] = useState(false);
  const toast = useToast();

  async function searchMovies(query: string) {
    setCompactMovieData([]);
    setMoviesWithTrailer([]);
    setErrorData("");
    setErrorFlag(false);
    const URL = "http://localhost:8000/api/v2/trailer/search";

    try {
      setIsLoading(true);
      const response = await fetch(
        `${URL}?title=${query}&network_lag=${networkLag}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        console.log("response headers:", response.headers);
        setCompactMovieData(data);

        const dataArray = [];

        for (const movie of data) {
          const response = await fetch(
            `${URL}/${movie.imdbid}?network_lag=${networkLag}`,
            {
              method: "GET",
              headers: {
                "content-type": "application/json",
              },
            }
          );
          if (response.ok) {
            const result = await response.json();

            dataArray.push(result);
            setMoviesWithTrailer([...dataArray]);
          } else {
            setErrorData("Error fetching data..");
            setErrorFlag(true);
            console.log("error data: ", errorData);
            console.log("error flag:", errorFlag);
          }
        }
      } else {
        setErrorFlag(true);
        // toast({
        //   title: "Error fetching data!",
        //   description: "Movie not found!",
        //   status: "error",
        //   duration: 9000,
        //   isClosable: true,
        // });
      }
      if (errorFlag) {
        toast({
          title: "Error fetching data!",
          description: "Movie not found!",
          status: "error",
          duration: 9000,
          isClosable: true,
        });
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
          <Heading mb={4}>Search Trailers (mock) </Heading>
        </Flex>
        <Flex mb={4}>
          <Text>
            Available movies in mock: star wars, indiana jones, lord of the
            rings
          </Text>
        </Flex>
        <Flex gap={5} mb={3} alignItems={"center"}>
          <Text>Simulate network lag in seconds: </Text>
          <Input
            type="text"
            width="40px"
            variant="flushed"
            placeholder="1.2"
            flex="1"
            value={networkLag}
            onChange={(e) => setNetworkLag(e.target.value)}
            colorScheme="teal"
          />
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
      <Flex alignItems="center" flexDir="column">
        {isLoading && <Text> Loading {compactMovieData.length} movies...</Text>}
      </Flex>
      <Flex
        flexDir={"column"}
        gap={5}
        alignItems={"center"}
        flexDirection="column"
      >
        {moviesWithTrailer &&
          moviesWithTrailer.map((movie) => {
            if (!movie.title || !movie.trailerEmbedLink) {
              return;
            }
            return (
              <>
                <ScaleFade initialScale={0.3} in={true} key={movie.director}>
                  <MovieCardWithImage movie={movie} key={movie.imdbid} />
                </ScaleFade>
                <Divider
                  height={2}
                  w="600px"
                  colorScheme="teal"
                  key={movie.title}
                />
              </>
            );
          })}
        {isLoading && (
          <Center>
            {/* <Spinner size={"xl"} /> */}
            <Flex gap={30}>
              <Skeleton width="200px" height="160px" />
              <Stack>
                <Skeleton width="500px" height="20px" />
                <Skeleton width="500px" height="20px" />
                <Skeleton width="500px" height="20px" />
                <Skeleton width="500px" height="20px" />
                <Skeleton width="500px" height="20px" />
                <Skeleton width="500px" height="20px" />
                <Skeleton width="500px" height="20px" />
              </Stack>
            </Flex>
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
