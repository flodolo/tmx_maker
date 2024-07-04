# Variables:
#   $num - default value of the `dom.ipc.processCount` pref.
default-content-process-count =
    .label = { $num } (default)

empty-value = ''
    .label = Test

no-value =
    .label = Test

# Plural form
timeDiffHoursAgo = { $number ->
         [one] 1 hour ago
        *[other] { $number } hours ago
    }

# Basic string
sample = Just a test

some junk text, should be ignored

# Parameterized term
onboarding-fxa-text = Зарегистрируйте { -fxaccount-brand-name(case: "nominative") } test.
