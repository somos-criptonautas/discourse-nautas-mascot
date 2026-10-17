import { apiInitializer } from "discourse/lib/api";
import NautasMascot from "../components/nautas-mascot";

export default apiInitializer((api) => {
  api.renderInOutlet("search-menu-before-term-input", NautasMascot);
});
