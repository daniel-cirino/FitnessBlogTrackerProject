from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import UserRegistrationForm, EditProfileForm, EditProfileImageForm
from django.contrib.auth.decorators import login_required


def registration_form(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')  # Valid data, flash message
            messages.success(request, f'Account has been created!')
            return redirect('signin')
    else:
        form = UserRegistrationForm
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, instance=request.user)
        edit_profile_image_form = EditProfileImageForm(request.POST, request.FILES, instance=request.user.profile)

        if edit_profile_form.is_valid() and edit_profile_image_form.is_valid():
            edit_profile_form.save()
            edit_profile_image_form.save()
            messages.success(request, f'Updated!')
            return redirect('profile')

    else:
        edit_profile_form = EditProfileForm(instance=request.user)
        edit_profile_image_form = EditProfileImageForm(instance=request.user.profile)

    context = {
        'edit_profile_form': edit_profile_form,
        'edit_profile_image_form': edit_profile_image_form
    }
    return render(request, 'users/profile.html', context)


