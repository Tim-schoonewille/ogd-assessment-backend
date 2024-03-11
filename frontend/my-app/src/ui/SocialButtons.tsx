import { Flex, Icon } from "@chakra-ui/react";
import {
  EmailIcon,
  EmailShareButton,
  FacebookIcon,
  FacebookShareButton,
  LinkedinIcon,
  LinkedinShareButton,
  RedditIcon,
  RedditShareButton,
  TelegramIcon,
  TelegramShareButton,
  TwitterIcon,
  TwitterShareButton,
  WhatsappIcon,
  WhatsappShareButton,
} from "react-share";
import { MovieDataWithTrailer } from "../types";

type SocialButtonsProps = {
  movie: MovieDataWithTrailer;
};
export default function SocialButtons({ movie }: SocialButtonsProps) {
  const roundness = 10;
  return (
    <Flex gap="2">
      <EmailShareButton url={movie.trailerLink}>
        <Icon
          as={EmailIcon}
          rounded={roundness}
          _hover={{ cursor: "pointer", transform: "translateY(-2px)" }}
        />
      </EmailShareButton>
      <WhatsappShareButton
        title={`${movie.title} trailer`}
        url={movie.trailerLink}
      >
        <Icon as={WhatsappIcon} rounded={roundness} />
      </WhatsappShareButton>
      <FacebookShareButton url={movie.trailerLink}>
        <Icon as={FacebookIcon} rounded={roundness} />
      </FacebookShareButton>
      <TwitterShareButton url={movie.trailerLink}>
        <Icon as={TwitterIcon} rounded={roundness} />
      </TwitterShareButton>
      <LinkedinShareButton url={movie.trailerLink}>
        <Icon as={LinkedinIcon} rounded={roundness} />
      </LinkedinShareButton>

      <RedditShareButton url={movie.trailerLink}>
        <Icon as={RedditIcon} rounded={roundness} />
      </RedditShareButton>
      <TelegramShareButton url={movie.trailerLink}>
        <Icon as={TelegramIcon} rounded={roundness} />
      </TelegramShareButton>
    </Flex>
  );
}
