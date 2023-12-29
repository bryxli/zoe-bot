import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Information from "@/components/Information";

describe("Header", () => {
  it("renders Header", () => {
    const container = render(
      <AuthProvider>
        <GuildProvider>
          <Information />
        </GuildProvider>
      </AuthProvider>,
    ).container;

    expect(container.getElementsByClassName("Information").length).toBe(1);
  });
});
