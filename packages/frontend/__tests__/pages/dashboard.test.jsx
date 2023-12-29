import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

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
    render(
      <AuthProvider>
        <GuildProvider>
          <Dashboard />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Dashboard");

    expect(component).toBeInTheDocument();
  });
});
