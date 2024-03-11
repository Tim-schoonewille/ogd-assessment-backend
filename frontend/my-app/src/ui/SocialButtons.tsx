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

type SocialButtonsProps = {
  link: string;
};
export default function SocialButtons({ link }: SocialButtonsProps) {
  return (
    <Flex gap="1">
      <EmailShareButton url={link}>
        <Icon as={EmailIcon} />
      </EmailShareButton>
      <WhatsappShareButton url={link}>
        <Icon as={WhatsappIcon} />
      </WhatsappShareButton>
      <FacebookShareButton url={link}>
        <Icon as={FacebookIcon} />
      </FacebookShareButton>
      <TwitterShareButton url={link}>
        <Icon as={TwitterIcon} />
      </TwitterShareButton>
      <LinkedinShareButton url={link}>
        <Icon as={LinkedinIcon} />
      </LinkedinShareButton>
      <RedditShareButton url={link}>
        <Icon as={RedditIcon} />
      </RedditShareButton>
      <TelegramShareButton url={link}>
        <Icon as={TelegramIcon} />
      </TelegramShareButton>
    </Flex>
  );
}
