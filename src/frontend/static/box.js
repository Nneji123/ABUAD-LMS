$(document).ready(function() {
    $('#example').DataTable();
} );

$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});