import { Button, Col, Form, Row } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function Reset({ data, setGuild, setData }: DataComponentProps) {
  const reset = async (event: any) => {
    event.preventDefault();

    const confirm = event.target.confirm.value;

    if (confirm === "delete") {
      const res = await fetch("/api/discord/webhook", {
        method: "DELETE",
        body: JSON.stringify({
          id: data.body.webhookId,
        }),
      });

      const updatedGuild = await fetch("/api/dynamo/reset", {
        method: "POST",
        body: JSON.stringify({
          guild: { guild_id: data.body.guildId },
        }),
      }).then((result) => result.json());

      setGuild(updatedGuild);
      setData({ command: "", body: {} });
    }
  };

  return (
    <div data-testid="Reset">
      <Form onSubmit={reset}>
        <Form.Group className="mb-3">
          <Form.Control
            name="confirm"
            placeholder="Please type 'delete' to reset"
          />
          <br></br>
          <Button
            type="submit"
            className="authButton"
            style={{ position: "absolute", bottom: 10 }}
          >
            /reset
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}
