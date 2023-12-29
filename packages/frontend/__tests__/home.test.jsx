import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Home from "@/page";

describe("Home", () => {
  let container;

  beforeEach(() => {
    fetch.resetMocks();

    const component = render(
      <AuthProvider>
        <GuildProvider>
          <Home />
        </GuildProvider>
      </AuthProvider>,
    );

    container = component.container;
  });

  it("renders Home", async () => {
    fetch.mockResponseOnce(JSON.stringify("api started"));

    expect(container.getElementsByClassName("Home").length).toBe(1);
  });
});
