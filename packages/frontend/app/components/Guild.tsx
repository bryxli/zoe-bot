"use client";

import { Card } from "react-bootstrap";

import { GuildProps } from "../types";

export default function Guild({
  id,
  name,
  icon,
  owner,
  permissions,
  permissions_new,
  features,
}: GuildProps) {
  const handleCardClick = () => {
    console.log("TODO: Create modal");
  };

  return (
    <Card style={{ cursor: "pointer" }} onClick={handleCardClick}>
      <Card.Body>
        <Card.Title> {name} </Card.Title>
      </Card.Body>
    </Card>
  );
}
