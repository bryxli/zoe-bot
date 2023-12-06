import { Container, Row } from "react-bootstrap";

export default function Information() {
  return (
    <Container className="d-flex flex-column align-items-center justify-content-center information">
      <Row>zoe traverses through the rift to find info about you. zoe will broadcast wins and losses every five minutes.</Row>
    <Row>Commands</Row>
    <Row>/help - command list</Row>
    <Row>/setup - create guild instance</Row>
    <Row>/reset - reset instance</Row>
    <Row>/region - change guild region</Row>
    <Row>/acknowledge - acknowledge dangerous commands</Row>
    <Row>/adduser &lt;username&gt; - add user to guild, user must be a valid League of Legends username</Row>
    <Row>/deluser &lt;username&gt; - delete user from guild, user must be a valid League of Legends username and exist</Row>
    <Row>/userlist - display guild userlist</Row>
    <Row className="mb-4">/speak - zoe will talk to you</Row>

        <p>
          Click{" "}
          <a href="https://discord.com/api/oauth2/authorize?client_id=1014214102459093105&permissions=2048&scope=bot">
            here
          </a>{" "}
          to invite to server.
        </p>
    </Container>
  );
}
