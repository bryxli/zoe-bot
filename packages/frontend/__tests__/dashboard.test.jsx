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
  it("renders Dashboard", () => {
    const container = render(
      <AuthProvider>
        <GuildProvider>
          <Dashboard />
        </GuildProvider>
      </AuthProvider>,
    ).container;

    expect(container.getElementsByClassName("Dashboard").length).toBe(1);
  });
});
