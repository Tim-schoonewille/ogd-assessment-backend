import { Box, Flex, Image, Text } from "@chakra-ui/react";
import { MovieDataWithTrailer } from "../types";

interface movieCardProps {
  movie: MovieDataWithTrailer;
}
const MovieCardWithImage: React.FC<movieCardProps> = ({ movie }) => {
  return (
    <Flex>
      <Image src={movie.poster} alt={movie.title} width="150px" />
      <Box maxW="md" borderWidth="1px" borderRadius="lg" overflow="hidden">
        <Box p="6">
          <Box display="flex" alignItems="baseline">
            <Text fontWeight="semibold" fontSize="lg">
              {movie.title} ({movie.year})
            </Text>
            <Text ml="2" color="gray.500" fontSize="sm">
              Rated: {movie.rated}
            </Text>
          </Box>

          <Text mt="2" color="gray.600" fontSize="sm">
            Genre: {movie.genre}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            Director: {movie.director}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            Runtime: {movie.runtime}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            Released: {movie.released}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            IMDb Rating: {movie.imdbrating}
          </Text>
          <Text mt="2" color="gray.600" fontSize="sm">
            Traier link: {movie.trailerLink}
          </Text>
        </Box>
      </Box>
      <Box>
        <iframe
          width="350"
          height="300"
          src={movie.trailerLink}
          title="YouTube video player"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        ></iframe>
      </Box>
    </Flex>
  );
};

export default MovieCardWithImage;
