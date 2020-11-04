program fdtd
    implicit none
    integer, parameter :: length=8
    real, parameter :: c0=299792458.
    real, dimension(length) :: epsilon_r, mu_r
    integer :: i

    ! Initialize materials to free space
    do i=1, length
        epsilon_r(i)=1
        mu_r(i)=1
    end do
    

    print *, epsilon_r
    print *, mu_r


end program fdtd