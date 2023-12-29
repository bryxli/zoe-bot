import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Home from "@/page";

describe("Home", () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it("renders Home", async () => {
    fetch.mockResponseOnce(JSON.stringify("api started"));

    const container = render(
      <AuthProvider>
        <GuildProvider>
          <Home />
        </GuildProvider>
      </AuthProvider>,
    ).container;

    expect(container.getElementsByClassName("Home").length).toBe(1);
  });
});
