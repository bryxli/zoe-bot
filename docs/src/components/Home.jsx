import React from "react";

const Home = () => {
  return (
    <div>
      <ul>
        <p>
          zoe will let you know when you win or lose. i guess she is just that
          smart. zoe checks every five minutes, she can't be doing it all day!
        </p>
        <p>zoe shouts out game results in her channel.</p>
      </ul>

      <ul>
        <p>
          <strong>Commands</strong>
        </p>
        <li>
          ?setup - zoe will speak in this channel <b>(run this first)</b>
        </li>
        <li>?reset - wipe server from database</li>
        <li>?region - list current region and region codes</li>
        <li>?setregion &lt;region&gt;- set server region</li>
        <li>?adduser &lt;league username&gt; - add to server database</li>
        <li>?deluser &lt;league username&gt; - delete from server database</li>
        <li>?userlist - show server userlist</li>
        <li>?speak - zoe will talk to you</li>
        <li>?help - help menu</li>
      </ul>

      <ul>
        <p>
          Click{" "}
          <a href="https://discord.com/api/oauth2/authorize?client_id=1014214102459093105&permissions=2048&scope=bot">
            here
          </a>{" "}
          to invite to server.
        </p>
      </ul>
    </div>
  );
};

export default Home;
