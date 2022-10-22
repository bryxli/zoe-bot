import React, { useEffect, useState } from "react";
import CustomCard from "./CustomCard";

const MasterOutput = () => {
  const [gameList, setGameList] = useState(0);

  useEffect(() => {
    fetch("/data").then((response) =>
      response.json().then((data) => {
        setGameList(data.games);
      })
    );
  }, []);

  const games = Array.from(gameList);
  var cards = [];
  for (const game of games) {
    const card = <CustomCard detail={game} key={game} />;
    cards.push(card);
  }

  return (
    <div>
      <ul className="customCard">{cards}</ul>
    </div>
  );
};

export default MasterOutput;
