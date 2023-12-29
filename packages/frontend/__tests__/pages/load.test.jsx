import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthContext } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Load from "@/load/page";

jest.mock("next/navigation", () => ({
  useRouter() {
    return {
      push: () => null,
    };
  },
}));

describe("Load", () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it("renders Load", async () => {
    fetch.mockResponse(JSON.stringify(null));

    const signIn = jest.fn();

    render(
      <AuthContext.Provider value={{ signIn }}>
        <GuildProvider>
          <Load />
        </GuildProvider>
      </AuthContext.Provider>,
    );

    const component = screen.getByTestId("Load");

    expect(component).toBeInTheDocument();
  });
});
