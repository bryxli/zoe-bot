import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Dashboard from "@/dashboard/page";

jest.mock("next/navigation", () => ({
  useRouter() {
    return {
      push: () => null,
    };
  },
}));

describe("Dashboard", () => {
  let container;

  beforeEach(() => {
    const component = render(
      <AuthProvider>
        <GuildProvider>
          <Dashboard />
        </GuildProvider>
      </AuthProvider>,
    );

    container = component.container;
  });

  it("renders Dashboard", () => {
    expect(container.getElementsByClassName("Dashboard").length).toBe(1);
  });
});
