// BCE Boundary tests: :SearchUserProfilePage
// Covers: displayProfileFound, displayProfileNotFound, controller call with keyword

// ─── Imports ────────────────────────────────────────────────────────────────────
// Vitest globals: describe/it/expect group and define tests; vi handles mocking;
// beforeEach runs setup code before every individual test.
import { describe, it, expect, vi, beforeEach } from 'vitest'

// render     — mounts a React component into a virtual DOM for testing
// screen     — queries the rendered output (getByText, getByRole, etc.)
// waitFor    — retries an assertion until it passes or times out (handles async state)
import { render, screen, waitFor } from '@testing-library/react'

// Simulates real user interactions (typing, clicking) with proper event sequencing
import userEvent from '@testing-library/user-event'

// MemoryRouter provides React Router context without a real browser URL bar.
// Required because UserProfileManagementPage uses useNavigate() internally.
import { MemoryRouter } from 'react-router-dom'

// The component under test — this is the BCE Boundary: :SearchUserProfilePage
import UserProfileManagementPage from '../pages/UserProfileManagementPage'

// ─── Mocks ──────────────────────────────────────────────────────────────────────

// Replace the real API module with a fake so tests never make HTTP calls to the backend.
// vi.fn() creates a spy function whose return value we control per-test.
vi.mock('../api/userProfileApi', () => ({
  searchUserProfile: vi.fn(),
}))

// Sidebar uses useAuth() which requires AuthContext to be provided.
// Rather than setting up the full auth context, we stub Sidebar with an empty div.
// This keeps the test focused on the page logic, not the sidebar's dependencies.
vi.mock('../components/Sidebar', () => ({
  default: () => <div data-testid="sidebar" />,
}))

// Import the mocked version of searchUserProfile so we can control its return
// value and inspect how it was called in each test.
import { searchUserProfile } from '../api/userProfileApi'

// ─── Helper ─────────────────────────────────────────────────────────────────────

// Wraps the page in MemoryRouter every time so useNavigate() inside the component
// has a valid router context. Avoids repeating this boilerplate in each test.
function renderPage() {
  return render(
    <MemoryRouter>
      <UserProfileManagementPage />
    </MemoryRouter>
  )
}

// ─── Test suite ─────────────────────────────────────────────────────────────────

describe('UserProfileManagementPage — BCE Boundary: :SearchUserProfilePage', () => {

  // Runs before every individual test:
  // 1. vi.clearAllMocks() resets call counts so one test's calls don't bleed into the next.
  // 2. mockResolvedValue([]) sets the default response for the initial mount-time
  //    loadAll() call — the component calls searchUserProfile('') on first render.
  beforeEach(() => {
    vi.clearAllMocks()
    searchUserProfile.mockResolvedValue([])
  })

  // ── Test 1 ──────────────────────────────────────────────────────────────────
  // Verifies the basic UI structure: the search input and Search button are present.
  // waitFor is used first to let the async loadAll() on mount finish, so React
  // does not warn about state updates happening outside act().
  it('renders the search input and Search button', async () => {
    renderPage()

    // Wait until the mount-time API call completes before querying the DOM
    await waitFor(() => expect(searchUserProfile).toHaveBeenCalledWith(''))

    // The SearchBar component renders an <input> with this exact placeholder text
    expect(
      screen.getByPlaceholderText('Search by User ID, User Name......')
    ).toBeInTheDocument()

    // The SearchBar renders a submit button with visible text "Search"
    expect(
      screen.getByRole('button', { name: 'Search' })
    ).toBeInTheDocument()
  })

  // ── Test 2 ──────────────────────────────────────────────────────────────────
  // Verifies the controller is called with the correct keyword when the user
  // types in the search box and clicks Search.
  it('calls searchUserProfile with the typed keyword on submit', async () => {
    // userEvent.setup() creates a user-event instance that properly sequences
    // pointer and keyboard events the way a real browser would
    const user = userEvent.setup()
    renderPage()

    // Let the initial loadAll() finish before simulating user interaction
    await waitFor(() => expect(searchUserProfile).toHaveBeenCalledWith(''))

    // Simulate the user typing "donee" into the search input
    await user.type(
      screen.getByPlaceholderText('Search by User ID, User Name......'),
      'donee'
    )

    // Simulate the user clicking the Search button to submit the form
    await user.click(screen.getByRole('button', { name: 'Search' }))

    // Assert that the API was called with exactly the keyword the user typed
    await waitFor(() => {
      expect(searchUserProfile).toHaveBeenCalledWith('donee')
    })
  })

  // ── Test 3 ──────────────────────────────────────────────────────────────────
  // Covers the displayProfileFound() boundary method.
  // When the API returns profiles, a card should appear for each one showing
  // the profile name.
  it('displayProfileFound — renders a card for each returned profile', async () => {
    // Define the fake data that the mocked API will return for this test only
    const mockProfiles = [
      { profileID: 1, profileName: 'Donee', profileDescription: 'Donee role', profileStatus: 'Active' },
      { profileID: 2, profileName: 'Fund Raiser', profileDescription: 'Fund raiser role', profileStatus: 'Active' },
    ]

    // Override the default mock so this specific search returns our fake profiles
    searchUserProfile.mockResolvedValue(mockProfiles)

    const user = userEvent.setup()
    renderPage()

    await user.type(
      screen.getByPlaceholderText('Search by User ID, User Name......'),
      'donee'
    )
    await user.click(screen.getByRole('button', { name: 'Search' }))

    // After the async search resolves, both profile names should be visible in the DOM
    await waitFor(() => {
      expect(screen.getByText('Donee')).toBeInTheDocument()
      expect(screen.getByText('Fund Raiser')).toBeInTheDocument()
    })
  })

  // ── Test 4 ──────────────────────────────────────────────────────────────────
  // Covers the displayProfileNotFound() boundary method.
  // When the API returns an empty array, the component should show the
  // "No profiles found." empty-state message instead of a list.
  it('displayProfileNotFound — shows empty-state message when results are empty', async () => {
    // The beforeEach already sets the default to [], but we set it explicitly
    // here for clarity — this test is specifically about the empty-result path
    searchUserProfile.mockResolvedValue([])

    const user = userEvent.setup()
    renderPage()

    await user.type(
      screen.getByPlaceholderText('Search by User ID, User Name......'),
      'nonexistent'
    )
    await user.click(screen.getByRole('button', { name: 'Search' }))

    // The exact string "No profiles found." comes from the component's empty state UI
    await waitFor(() => {
      expect(screen.getByText('No profiles found.')).toBeInTheDocument()
    })
  })
})
