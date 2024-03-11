import {
  Box,
  Button,
  Flex,
  Image,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import { MovieDataWithTrailer } from "../types";
import { useState } from "react";
import { IoMdShare, IoMdVideocam } from "react-icons/io";
import {
  EmailIcon,
  EmailShareButton,
  WhatsappIcon,
  WhatsappShareButton,
} from "react-share";
import SocialButtons from "./SocialButtons";
interface movieCardProps {
  movie: MovieDataWithTrailer;
}

const MovieCardWithImage: React.FC<movieCardProps> = ({ movie }) => {
  const [showTrailer, setShowTrailer] = useState(false);
  const { isOpen, onOpen, onClose } = useDisclosure();
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
          <Flex gap={2}>
            <Button
              leftIcon={<IoMdVideocam />}
              mt={3}
              size={"xs"}
              colorScheme="teal"
              variant={showTrailer ? "outline" : "solid"}
              onClick={() => setShowTrailer(!showTrailer)}
            >
              {showTrailer ? "Hide" : "Show"} Trailer
            </Button>
            <Button
              leftIcon={<IoMdShare />}
              mt={3}
              size={"xs"}
              colorScheme="teal"
              variant="solid"
              onClick={onOpen}
            >
              Share
            </Button>
            <Modal
              isCentered
              onClose={onClose}
              isOpen={isOpen}
              motionPreset="slideInBottom"
              size="xs"
            >
              <ModalOverlay
                bg="blackAlpha.300"
                backdropFilter="blur(10px) hue-rotate(90deg)"
              />
              <ModalContent>
                <ModalHeader>Share on social!</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                  <SocialButtons link={movie.trailerLink} />
                </ModalBody>
                <ModalFooter>
                  <Button size="xs" colorScheme="red" mr={3} onClick={onClose}>
                    Close
                  </Button>
                </ModalFooter>
              </ModalContent>
            </Modal>
          </Flex>
        </Box>
      </Box>
      {showTrailer && (
        <Box>
          <iframe
            width="350"
            height="280"
            src={movie.trailerLink}
            title="YouTube video player"
            allowFullScreen
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          ></iframe>
        </Box>
      )}
    </Flex>
  );
};

export default MovieCardWithImage;
