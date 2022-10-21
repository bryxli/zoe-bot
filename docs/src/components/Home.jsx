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
        <div>Commands</div>
        <div>?setup - zoe will speak in this channel (run this first)</div>
        <div>?reset - wipe server from database</div>
        <div>?region - list current region and region codes</div>
        <div>?setregion &lt;region&gt;- set server region</div>
        <div>?adduser &lt;league username&gt; - add to server database</div>
        <div>?deluser &lt;league username&gt; - delete from server database</div>
        <div>?userlist - show server userlist</div>
        <div>?speak - zoe will talk to you</div>
        <div>?help - help menu</div>
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