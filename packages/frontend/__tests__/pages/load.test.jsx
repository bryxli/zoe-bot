import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

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

    const signOut = jest.fn();

    const userInfo = null;

    const container = render(
      <AuthContext.Provider value={{ signIn, signOut, userInfo }}>
        <GuildProvider>
          <Load />
        </GuildProvider>
      </AuthContext.Provider>,
    ).container;

    expect(container.getElementsByClassName("Load").length).toBe(1);
  });
});
