import React from "react";
import Card from "react-bootstrap/Card";

const CustomCard = (detail) => {
  return (
    <Card>
      <Card.Body>
        <Card.Text>{detail["detail"]}</Card.Text>
      </Card.Body>
    </Card>
  );
};

export default CustomCard;
