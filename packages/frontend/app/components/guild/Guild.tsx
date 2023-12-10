"use client";

import { useState } from "react";
import { Card } from "react-bootstrap";
import { GuildProps } from "../../types";
import GuildModal from "./GuildModal";

export default function Guild({
  id,
  name,
  icon,
  owner,
  permissions,
  permissions_new,
  features,
}: GuildProps) {
  const [showModal, setShowModal] = useState(false);

  const display = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <Card style={{ cursor: "pointer" }} onClick={display}>
        <Card.Body>
          <Card.Title> {name} </Card.Title>
        </Card.Body>
      </Card>
      <GuildModal
        showModal={showModal}
        onHide={display}
        id={id}
        name={name}
        icon={icon}
      />
    </>
  );
}
