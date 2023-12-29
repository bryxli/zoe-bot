import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Home from "@/page";

describe("Home", () => {
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  it("renders readable section", async () => {
    const res = "api started";

    fetchMock.mockResolvedValue({ status: 200, json: jest.fn(() => res) });

    const { container } = render(
      <AuthProvider>
        <GuildProvider>
          <Home />
        </GuildProvider>
      </AuthProvider>,
    );

    expect(container.getElementsByClassName("readable").length > 0);
  });
});
