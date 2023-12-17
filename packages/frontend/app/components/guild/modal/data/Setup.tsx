import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/app/types";

export default function Setup({ data, setGuild, setData }: DataComponentProps) {
  const setup = async (event: any) => {
    event.preventDefault();
    const channelId = event.target.id.value;

    const webhook = await fetch("/api/discord/webhook", {
      method: "POST",
      body: JSON.stringify({
        id: channelId,
      }),
    }).then((result) => result.json());

    const guild = await fetch("/api/dynamo/setup", {
      method: "POST",
      body: JSON.stringify({
        id: data.body,
        webhook: webhook,
      }),
    }).then((result) => result.json());

    setGuild(guild);
    setData({ command: "", body: "" });
  };

  return (
    <Form onSubmit={setup}>
      <Form.Group className="mb-3">
        <Form.Control name="id" placeholder="Discord Channel ID" />
        <br></br>
        <Button
          type="submit"
          className="authButton"
          style={{ position: "absolute", bottom: 10 }}
        >
          /setup
        </Button>
      </Form.Group>
    </Form>
  );
}
