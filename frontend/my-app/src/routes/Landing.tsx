import { Button, Fade, Flex, Heading, ScaleFade } from "@chakra-ui/react";
import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <>
      <Flex
        flexDir={"column"}
        alignItems={"center"}
        justifyContent="center"
        minHeight="100vh"
      >
        <ScaleFade in={true} initialScale={0.01}>
          <Heading mb={5}>Search trailerss</Heading>
          <Flex gap={5}>
            <Link to={"/v2/search"}>
              <Button colorScheme="teal" size="lg">
                V2
              </Button>
            </Link>
            <Link to="/mock/search">
              <Button colorScheme="teal" size="lg">
                Mock V2
              </Button>
            </Link>
          </Flex>
        </ScaleFade>
      </Flex>
    </>
  );
}
