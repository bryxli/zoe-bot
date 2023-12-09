import { useEffect, useState } from "react";
import { Container, Modal, Row } from "react-bootstrap";
import Image from "next/image";

import { GuildModalProps } from "../types";

export default function GuildModal({
  showModal,
  onHide,
  id,
  name,
  icon,
}: GuildModalProps) {
  const [userlist, setUserlist] = useState<string[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      await fetch("/api/dynamo/userlist", {
        method: "POST",
        body: JSON.stringify({
          guildId: id,
        }),
      })
        .then((result) => result.json())
        .then((response) => {
          setUserlist(response);
        });
    };

    fetchUsers();
  }, [id]);

  return (
    <Modal show={showModal} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>
          {name}
          {icon && (
            <Image
              src={`https://cdn.discordapp.com/icons/${id}/${icon}.jpg`}
              alt="Guild Avatar"
              width={30}
              height={30}
              priority={true}
            />
          )}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          {userlist.length > 0
            ? userlist.map((user) => {
                return <Row key={user}>{user}</Row>;
              })
            : "userlist is empty"}
        </Container>
      </Modal.Body>
    </Modal>
  );
}
