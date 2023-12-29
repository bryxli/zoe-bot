import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Home from "@/page";

describe("Home", () => {
  let container;

  beforeEach(() => {
    fetchMock.resetMocks();

    const component = render(
      <AuthProvider>
        <GuildProvider>
          <Home />
        </GuildProvider>
      </AuthProvider>,
    );

    container = component.container;
  });

  it("renders readable section", async () => {
    const res = "api started";

    fetchMock.mockResolvedValue({ status: 200, json: jest.fn(() => res) });

    expect(container.getElementsByClassName("readable").length).toBe(0);
  });
});
