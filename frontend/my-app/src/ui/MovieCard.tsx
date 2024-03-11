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
      <Image
        src={movie.poster}
        alt={movie.title}
        width="150px"
        height="250px"
        mr={5}
      />
      <Box
        maxW="l"
        width="600px"
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
      >
        <Box p="6">
          <Box display="flex" alignItems="baseline">
            <Text fontWeight="semibold" fontSize="lg">
              {movie.title} ({movie.year})
            </Text>
            <Text ml="2" color="gray.500" fontSize="sm">
              {movie.rated}
            </Text>
          </Box>

          <Text mt="2" color="gray.600" fontSize="sm">
            <span style={{ fontWeight: "bold" }}>Genre:</span> {movie.genre}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            <span style={{ fontWeight: "bold" }}>Director:</span>{" "}
            {movie.director}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            <span style={{ fontWeight: "bold" }}>Runtime:</span> {movie.runtime}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            <span style={{ fontWeight: "bold" }}>Released:</span>{" "}
            {movie.released}
          </Text>

          <Text mt="2" color="gray.600" fontSize="sm">
            <span style={{ fontWeight: "bold" }}>IMDb Rating:</span>{" "}
            {movie.imdbrating}
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
            {/* <Button
              leftIcon={<IoMdShare />}
              mt={3}
              size={"xs"}
              colorScheme="teal"
              variant="solid"
              onClick={onOpen}
            >
              Share
            </Button> */}
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
                  <SocialButtons movie={movie} />
                </ModalBody>
                <ModalFooter>
                  <Button size="xs" colorScheme="red" mr={3} onClick={onClose}>
                    Close
                  </Button>
                </ModalFooter>
              </ModalContent>
            </Modal>
          </Flex>
          <Box mt={2}>
            <SocialButtons movie={movie} />
          </Box>
        </Box>
      </Box>
      {showTrailer && (
        <Box>
          <iframe
            width="450"
            height="280"
            src={movie.trailerEmbedLink}
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
